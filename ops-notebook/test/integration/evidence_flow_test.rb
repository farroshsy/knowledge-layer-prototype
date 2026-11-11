require "test_helper"

class EvidenceFlowTest < ActionDispatch::IntegrationTest
  test "budiono does not match budi and a plan is not an occurrence" do
    notebook = Notebook.create!(name: "uji")
    BusinessRecord.create!(notebook: notebook, kind: "person", display_name: "Budi", status: "unknown")
    budiono = BusinessRecord.create!(notebook: notebook, kind: "person", display_name: "Budiono", status: "occurred")
    pilot = BusinessRecord.create!(notebook: notebook, kind: "work_item", display_name: "pilot", status: "planned")

    budiono_answer = Evidence.ask(notebook, "Apa status Budiono?")
    assert_equal "db_only", budiono_answer.route
    assert_equal "occurred", budiono_answer.answer
    assert_equal [budiono.public_id], budiono_answer.records.map(&:public_id)
    assert_equal false, budiono_answer.semantic

    budi_answer = Evidence.ask(notebook, "Apa status Budi?")
    assert_equal ["Budi"], budi_answer.records.map(&:display_name)

    plan = Evidence.ask(notebook, "Apakah pekerjaan pilot sudah terjadi?")
    assert_equal "db_only", plan.route
    assert_equal "plan_not_occurrence", plan.answer
    assert_equal [pilot.public_id], plan.records.map(&:public_id)
  end

  test "document plan keeps its code and does not include attendance" do
    notebook = Notebook.create!(name: "dokumen")
    BusinessRecord.create!(notebook: notebook, kind: "work_item", display_name: "pilot", status: "planned")
    Evidence.upload(
      notebook,
      "baru.txt",
      "Notulen rapat operasional\n\nPeserta: Sari, Budi\nKeputusan: pilot direncanakan mulai 15 November. Kode HTTP-RAILS-1.\nMenurut Saksi A, Budi tidak hadir di rapat 14 Maret.\n"
    )
    answer = Evidence.ask(notebook, "Apakah pilot sudah berjalan?")
    quotes = answer.claims.map(&:quote).join(" ")
    assert_equal "document_only", answer.route
    assert_equal "plan_not_occurrence", answer.answer
    assert_includes quotes, "15 November"
    assert_includes quotes, "HTTP-RAILS-1"
    assert_not_includes quotes, "tidak hadir"
    peserta = ExtractedField.active.find_by!(document: notebook.documents.last, name: "peserta")
    assert_equal "Sari, Budi", peserta.value
    keputusan = ExtractedField.active.find_by!(document: notebook.documents.last, name: "keputusan")
    assert_equal "pilot direncanakan mulai 15 November. Kode HTTP-RAILS-1.", keputusan.value

    denial = Evidence.ask(notebook, "Apakah Budi hadir?")
    assert_equal "negated", denial.answer
    assert_includes denial.claims.map(&:quote).join(" "), "tidak hadir"
  end

  test "combined evidence requires the exact record id" do
    notebook = Notebook.create!(name: "gabungan")
    record = BusinessRecord.create!(notebook: notebook, kind: "work_item", display_name: "Onboarding", status: "planned")
    twin = BusinessRecord.create!(notebook: notebook, kind: "work_item", display_name: "Onboarding", status: "unknown")
    Evidence.upload(notebook, "memo.txt", "Keputusan: Onboarding dengan ID #{record.public_id} direncanakan mulai 23 November.")

    linked = Evidence.ask(notebook, "Apa status record #{record.public_id} menurut dokumennya?")
    assert_equal "combined", linked.route
    assert_equal [record.public_id], linked.records.map(&:public_id)
    assert linked.claims.all? { |claim| claim.quote.include?(record.public_id) }

    missing = Evidence.ask(notebook, "Apa status record #{twin.public_id} menurut dokumennya?")
    assert_equal "db_only", missing.route
    assert_equal "insufficient_evidence", missing.answer
    assert_equal [], missing.claims
  end

  test "user correction survives reprocess and notebooks stay separate" do
    home = Notebook.create!(name: "rumah")
    other = Notebook.create!(name: "lain")
    document = Evidence.upload(home, "campuran.txt", "Notulen rapat\n\nPeserta: Sari\n\nSOP dapur\n\nLangkah: Cuci bahan.\n")
    notulen = document.sections.order(:ordinal).first
    assert_equal "notulen", notulen.active_classification.category
    Evidence.correct(notulen, "other")
    Evidence.reprocess(document)
    notulen.reload
    assert_equal "other", notulen.active_classification.category
    assert_equal "user", notulen.active_classification.method
    assert_equal 0, notulen.extracted_fields.active.count
    sop = document.sections.order(:ordinal).last
    assert_equal "sop", sop.active_classification.category

    BusinessRecord.create!(notebook: home, kind: "person", display_name: "Sari", status: "unknown")
    isolated = Evidence.ask(other, "Apa status Sari?")
    assert_equal "abstain", isolated.answer
    assert_equal [], isolated.records
  end

  test "workbench page creates a record and answers from postgres" do
    post notebooks_path, params: { name: "Demo Rails" }
    notebook = Notebook.last
    assert_redirected_to root_path(notebook_id: notebook.id)
    post notebook_records_path(notebook), params: { kind: "person", display_name: "Budiono", status: "occurred" }
    get root_path(notebook_id: notebook.id)
    assert_response :success
    assert_includes response.body, "Notebook operasional"
    assert_includes response.body, "Budiono"
    post notebook_query_path(notebook), params: { question: "Apa status Budiono?" }
    assert_response :success
    assert_includes response.body, "db_only"
    assert_includes response.body, "occurred"
    assert_includes response.body, "Pekerjaan"
  end

  test "sample product links the job to its quote and keeps a human decision" do
    post example_notebooks_path
    notebook = Notebook.order(:id).last
    assert_redirected_to root_path(notebook_id: notebook.id)
    follow_redirect!
    assert_response :success
    onboarding = notebook.business_records.find_by!(display_name: "Onboarding karyawan")
    assert_equal "planned", onboarding.status
    assert_includes response.body, onboarding.public_id
    assert_includes response.body, "pekerjaan terbuka"
    assert_includes response.body, "diterima"

    linked = Evidence.ask(notebook, "Apa status record #{onboarding.public_id} menurut dokumennya?")
    assert_equal "combined", linked.route
    assert_equal "planned", linked.answer

    pilot = Evidence.ask(notebook, "Apakah pilot sudah berjalan?")
    assert_equal "plan_not_occurrence", pilot.answer
    assert_equal "planned", notebook.business_records.find_by!(display_name: "pilot").status
  end

  test "status change needs a note and a rejected quote stays rejected" do
    notebook = Notebook.create!(name: "keputusan")
    record = BusinessRecord.create!(notebook: notebook, kind: "work_item", display_name: "pilot", status: "planned")
    error = assert_raises(Evidence::Error) { Evidence.change_status(record, "occurred", " ") }
    assert_equal "keputusan butuh catatan", error.message
    assert_equal "planned", record.reload.status

    Evidence.change_status(record, "occurred", "Ditutup oleh penanggung jawab pada rapat internal.")
    assert_equal "occurred", record.reload.status
    assert_equal "status_changed", record.review_decisions.last.decision

    document = Evidence.upload(notebook, "rapat.txt", "Menurut Saksi A, Budi tidak hadir di rapat 14 Maret.\n")
    claim = document.claims.active.find { |row| row.quote.include?("tidak hadir") }
    Evidence.decide_claim(claim, "rejected", "Saksi tidak dipakai.")
    denied = Evidence.ask(notebook, "Apakah Budi hadir?")
    assert_equal "abstain", denied.answer

    Evidence.reprocess(document)
    fresh = document.claims.active.find { |row| row.quote.include?("tidak hadir") }
    assert_equal "rejected", fresh.latest_review.decision
    assert_equal "abstain", Evidence.ask(notebook, "Apakah Budi hadir?").answer
  end

  test "batch dump stores each text file and shows the document layers" do
    post notebooks_path, params: { name: "Dump" }
    notebook = Notebook.last
    post notebook_documents_path(notebook), params: {
      batch: [
        { filename: "sop-klien.txt", body: "SOP dapur\n\nLangkah: Cuci bahan.\n" },
        { filename: "rapat-klien.md", body: "Notulen rapat klien\n\nPeserta: Sari\n" }
      ].to_json
    }
    assert_redirected_to notebook_proses_path(notebook)
    follow_redirect!
    assert_response :success
    assert_includes response.body, "sop-klien.txt"
    assert_includes response.body, "rapat-klien.md"
    assert_includes response.body, "jenis file"
    assert_includes response.body, "Baris struktur"
    assert_equal 2, notebook.documents.count
    assert_equal "sop", notebook.documents.find_by!(filename: "sop-klien.txt").sections.first.active_classification.category
    assert_equal "notulen", notebook.documents.find_by!(filename: "rapat-klien.md").sections.first.active_classification.category
  end

  test "reading stages live on separate pages" do
    post example_notebooks_path
    notebook = Notebook.order(:id).last
    get notebook_proses_path(notebook)
    assert_response :success
    assert_includes response.body, "Rencana pembacaan"
    assert_includes response.body, "Skema isian"
    assert_includes response.body, "Kolom yang tidak tertulis tidak dibuat"
    assert_includes response.body, "Label belum dikenal"
    assert_not_includes response.body, "id=\"upload-body\""
    get notebook_analisis_path(notebook)
    assert_response :success
    assert_includes response.body, "Jenis isi"
    get notebook_keputusan_path(notebook)
    assert_response :success
    assert_includes response.body, "Bentrok"
    get notebook_verifikasi_path(notebook)
    assert_response :success
    assert_includes response.body, "Kutipan masih ada di teks sumber."
    get notebook_tanya_path(notebook)
    assert_response :success
    assert_includes response.body, "Tanya"
    assert_not_includes response.body, "id=\"upload-body\""
  end

  test "category consensus abstains when raters disagree and ignores the filename" do
    notebook = Notebook.create!(name: "konsensus")
    mixed = Evidence.upload(notebook, "sop-palsu.txt", "Notulen rapat peserta keputusan.\nLangkah: Cuci bahan.")
    assert_equal "other", mixed.sections.first.active_classification.category
    assert_includes mixed.sections.first.active_classification.reason, "konsensus gagal"
    assert_equal "consensus", mixed.sections.first.active_classification.method

    named = Evidence.upload(notebook, "sop-rapat.txt", "Notulen rapat\n\nPeserta: Sari\n")
    assert_equal ["notulen", "notulen"], named.sections.order(:ordinal).map { |section| section.active_classification.category }
    assert_includes named.sections.first.active_classification.reason, "nama=sop, diabaikan"
  end

  test "designed files are held before ocr and oversized text is not stored" do
    post notebooks_path, params: { name: "Peta" }
    notebook = Notebook.last
    post notebook_documents_path(notebook), params: {
      batch: [
        { filename: "catatan.txt", body: "Notulen rapat\n\nPeserta: Sari\n", byte_size: 40 },
        { filename: "kontrak.pdf", body: "", byte_size: 2_400_000 },
        { filename: "slide.pptx", body: "", byte_size: 80_000 },
        { filename: "pindaian.png", body: "", byte_size: 400_000 },
        { filename: "besar.txt", body: "a" * 200_001, byte_size: 200_001 }
      ].to_json
    }
    assert_redirected_to notebook_pemetaan_path(notebook)
    follow_redirect!
    assert_response :success
    assert_includes response.body, "OCR hanya untuk halaman yang tidak punya lapisan teks"
    assert_includes response.body, "Bukan OCR"
    assert_includes response.body, "Pemotongan belum dijalankan"
    assert_equal ["catatan.txt"], notebook.documents.pluck(:filename)
    assert_equal "blocked", notebook.intakes.find_by!(filename: "kontrak.pdf").status
    assert_nil notebook.intakes.find_by!(filename: "besar.txt").document_id
  end

  test "a question reads structured rows under their heading and abstains otherwise" do
    notebook = Notebook.create!(name: "struktur")
    Evidence.upload(notebook, "rapat.md", "Notulen rapat\n\nPeserta: Sari dan Budi\n\nKeputusan\n\nLanjut minggu depan.\n")
    found = Evidence.ask(notebook, "Siapa peserta notulen?")
    assert_equal "document_only", found.route
    assert_equal false, found.semantic
    assert_includes found.answer, "Peserta: Sari dan Budi"
    assert_includes found.rows.first.heading, "Notulen rapat"
    missing = Evidence.ask(notebook, "Berapa anggaran proposal?")
    assert_equal "abstain", missing.answer
  end
end

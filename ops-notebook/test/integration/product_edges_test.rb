require "test_helper"

class ProductEdgesTest < ActionDispatch::IntegrationTest
  test "two work items with the same name are ambiguous" do
    notebook = Notebook.create!(name: "ganda")
    first = BusinessRecord.create!(notebook: notebook, kind: "work_item", display_name: "Onboarding", status: "planned")
    second = BusinessRecord.create!(notebook: notebook, kind: "work_item", display_name: "Onboarding", status: "unknown")

    answer = Evidence.ask(notebook, "Apa status Onboarding?")
    assert_equal "db_only", answer.route
    assert_equal "ambiguous", answer.answer
    assert_equal [first.public_id, second.public_id].sort, answer.records.map(&:public_id).sort
  end

  test "affirmed and negated attendance in one document conflict" do
    notebook = Notebook.create!(name: "bentrok")
    Evidence.upload(
      notebook,
      "rapat.txt",
      "Sari hadir di rapat 14 Maret.\nMenurut Saksi A, Budi tidak hadir di rapat 14 Maret.\n"
    )

    answer = Evidence.ask(notebook, "Apakah ada yang hadir?")
    quotes = answer.claims.map(&:quote)
    assert_equal "conflict", answer.answer
    assert_includes quotes, "Sari hadir di rapat 14 Maret."
    assert_includes quotes, "Menurut Saksi A, Budi tidak hadir di rapat 14 Maret."
  end

  test "needs_evidence on the only attendance claim abstains" do
    notebook = Notebook.create!(name: "tahan")
    document = Evidence.upload(notebook, "satu.txt", "Menurut Saksi A, Budi tidak hadir di rapat 14 Maret.\n")
    claim = document.claims.active.find { |row| row.predicate == "attendance" }
    Evidence.decide_claim(claim, "needs_evidence", "Butuh sumber kedua.")

    answer = Evidence.ask(notebook, "Apakah Budi hadir?")
    assert_equal "abstain", answer.answer
    assert_equal [], answer.claims
  end

  test "changing to the same status adds no review decision" do
    notebook = Notebook.create!(name: "diam")
    record = BusinessRecord.create!(notebook: notebook, kind: "work_item", display_name: "pilot", status: "planned")

    error = assert_raises(Evidence::Error) { Evidence.change_status(record, "planned", "Catatan peninjau.") }
    assert_equal "status tidak berubah", error.message
    assert_equal "planned", record.reload.status
    assert_equal 0, record.review_decisions.count
  end

  test "two people with the same name make attendance ambiguous" do
    notebook = Notebook.create!(name: "dua")
    first = BusinessRecord.create!(notebook: notebook, kind: "person", display_name: "Budi", status: "unknown")
    second = BusinessRecord.create!(notebook: notebook, kind: "person", display_name: "Budi", status: "unknown")
    Evidence.upload(notebook, "rapat.txt", "Menurut Saksi A, Budi tidak hadir di rapat 14 Maret.\n")

    answer = Evidence.ask(notebook, "Apakah Budi hadir?")
    assert_equal "ambiguous", answer.answer
    assert_equal [first.public_id, second.public_id].sort, answer.records.map(&:public_id).sort
  end

  test "multibyte text keeps the field on its own line" do
    notebook = Notebook.create!(name: "aksara")
    document = Evidence.upload(notebook, "aksara.txt", "Notulen\n\nPeserta: José, Sari\n")
    assert_equal "José, Sari", document.extracted_fields.active.find_by!(name: "peserta").value
  end

  test "sudah alone does not treat a plan as an occurrence" do
    notebook = Notebook.create!(name: "kata")
    record = BusinessRecord.create!(notebook: notebook, kind: "work_item", display_name: "pilot", status: "planned")
    answer = Evidence.ask(notebook, "Apa status pilot yang sudah tercatat?")
    assert_equal "planned", answer.answer
    assert_equal [record.public_id], answer.records.map(&:public_id)
  end

  test "the same document text is stored once" do
    notebook = Notebook.create!(name: "hash")
    body = "Notulen rapat\n\nPeserta: Sari\n"
    first = Evidence.upload(notebook, "a.txt", body)
    second = Evidence.upload(notebook, "b.txt", body)
    assert_equal first.id, second.id
    assert second.reused_upload
    assert_equal 1, notebook.documents.count
  end

  test "pilot plans on different dates conflict" do
    notebook = Notebook.create!(name: "tanggal")
    Evidence.upload(notebook, "november.txt", "Keputusan: pilot direncanakan mulai 15 November.\n")
    Evidence.upload(notebook, "desember.txt", "Keputusan: pilot direncanakan mulai 1 Desember.\n")
    pairs = Evidence.conflicts(notebook.claims.active.to_a)
    assert_equal 1, pairs.length
    assert_includes pairs.first[0].quote + pairs.first[1].quote, "15 November"
    assert_includes pairs.first[0].quote + pairs.first[1].quote, "1 Desember"
  end

  test "empty document text is rejected" do
    notebook = Notebook.create!(name: "kosong")
    error = assert_raises(Evidence::Error) { Evidence.upload(notebook, "kosong.txt", "  ") }
    assert_equal "teks dokumen kosong", error.message
    assert_equal 0, notebook.documents.count
  end
end

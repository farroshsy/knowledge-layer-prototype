class SampleWorkspace
  def self.create!
    notebook = Notebook.create!(name: "Operasional contoh")
    notebook.business_records.create!(kind: "person", display_name: "Budi", status: "unknown")
    budiono = notebook.business_records.create!(kind: "person", display_name: "Budiono", status: "unknown")
    notebook.business_records.create!(kind: "person", display_name: "Sari", status: "unknown")
    onboarding = notebook.business_records.create!(kind: "work_item", display_name: "Onboarding karyawan", status: "planned")
    notebook.business_records.create!(kind: "work_item", display_name: "pilot", status: "planned")
    Evidence.change_status(budiono, "occurred", "Rekaman orang ditutup dari catatan operasional, bukan dari kalimat rencana.")
    document = Evidence.upload(
      notebook,
      "rapat-contoh.txt",
      <<~TEXT
        Notulen rapat operasional

        Peserta: Sari, Budi
        Keputusan: pekerjaan Onboarding karyawan dengan ID #{onboarding.public_id} direncanakan mulai 23 November. Kode CONTOH-PROD-1.
        Menurut Saksi A, Budi tidak hadir di rapat 14 Maret.

        Proposal pilot

        Latar belakang: pilot masih berupa rencana dan belum berjalan.
      TEXT
    )
    denial = document.claims.active.find { |claim| claim.quote.include?("tidak hadir") }
    raise Evidence::Error.new("validation", "contoh tidak menemukan kutipan kehadiran") unless denial

    Evidence.decide_claim(denial, "accepted", "Kutipan penolakan kehadiran dipakai sebagai bukti.")
    Evidence.load_demo_fixtures(notebook)
    notebook
  end
end

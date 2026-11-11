require "test_helper"

class RecordRulesTest < ActiveSupport::TestCase
  test "business record rejects kind tempat and status selesai" do
    notebook = Notebook.create!(name: "uji")
    record = BusinessRecord.new(
      notebook: notebook,
      kind: "tempat",
      display_name: "Gudang",
      status: "selesai"
    )

    assert_not record.valid?
    assert record.errors[:kind].any?
    assert record.errors[:status].any?
  end

  test "created records get distinct 32-hex public ids" do
    notebook = Notebook.create!(name: "uji")
    first = BusinessRecord.create!(notebook: notebook, kind: "person", display_name: "Budi", status: "unknown")
    second = BusinessRecord.create!(notebook: notebook, kind: "person", display_name: "Budi", status: "unknown")

    assert_match(/\A[0-9a-f]{32}\z/, first.public_id)
    assert_match(/\A[0-9a-f]{32}\z/, second.public_id)
    assert_not_equal first.public_id, second.public_id
  end

  test "review decision without claim or business record is invalid" do
    notebook = Notebook.create!(name: "uji")
    decision = ReviewDecision.new(
      notebook: notebook,
      decision: "rejected",
      note: "tanpa sasaran",
      authority: "user"
    )

    assert_not decision.valid?
    assert decision.errors[:base].any?
  end

  test "review decision maybe is invalid" do
    notebook = Notebook.create!(name: "uji")
    record = BusinessRecord.create!(notebook: notebook, kind: "person", display_name: "Budi", status: "unknown")
    decision = ReviewDecision.new(
      notebook: notebook,
      business_record: record,
      decision: "maybe",
      note: "bukan pilihan",
      authority: "user"
    )

    assert_not decision.valid?
    assert decision.errors[:decision].any?
  end

  test "status changed decision saves with record note and statuses" do
    notebook = Notebook.create!(name: "uji")
    record = BusinessRecord.create!(notebook: notebook, kind: "work_item", display_name: "pilot", status: "planned")
    decision = ReviewDecision.new(
      notebook: notebook,
      business_record: record,
      decision: "status_changed",
      note: "Ditutup oleh penanggung jawab.",
      authority: "user",
      previous_status: "planned",
      next_status: "occurred"
    )

    assert decision.save
    assert_equal notebook.id, decision.notebook_id
    assert_equal record.id, decision.business_record_id
    assert_equal "status_changed", decision.decision
    assert_equal "Ditutup oleh penanggung jawab.", decision.note
    assert_equal "user", decision.authority
    assert_equal "planned", decision.previous_status
    assert_equal "occurred", decision.next_status
  end
end

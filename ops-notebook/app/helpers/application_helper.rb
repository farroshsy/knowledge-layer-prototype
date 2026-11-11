module ApplicationHelper
  DECISION_LABELS = {
    "accepted" => "diterima",
    "rejected" => "ditolak",
    "needs_evidence" => "bukti kurang",
    "status_changed" => "status diubah"
  }.freeze

  def decision_label(decision)
    DECISION_LABELS.fetch(decision.to_s, decision.to_s)
  end

  FILE_KINDS = {
    ".txt" => "teks",
    ".md" => "markdown",
    ".markdown" => "markdown"
  }.freeze

  def quote_held?(claim)
    claim.section&.body_text.to_s.include?(claim.quote.to_s)
  end

  def file_kind(filename)
    FILE_KINDS.fetch(File.extname(filename.to_s).downcase, "ekstensi tidak dikenal")
  end

  def review_badge(claim)
    review = claim.latest_review
    return "belum ditinjau" unless review

    decision_label(review.decision)
  end
end

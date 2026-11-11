module Evidence
  # Human authority. A later generation does not erase these decisions.
  module Review
    extend self

    def change_status(record, status, note)
      raise Error.new("validation", "status tidak dikenal") unless BusinessRecord::STATUSES.include?(status)
      raise Error.new("validation", "status tidak berubah") if record.status == status

      text = required_note(note)
      ActiveRecord::Base.transaction do
        previous = record.status
        record.update!(status: status)
        record.review_decisions.create!(
          notebook: record.notebook,
          decision: "status_changed",
          note: text,
          authority: "user",
          previous_status: previous,
          next_status: status
        )
      end
      record
    end

    def decide_claim(claim, decision, note)
      raise Error.new("validation", "keputusan klaim tidak dikenal") unless ReviewDecision::CLAIM_DECISIONS.include?(decision)

      claim.review_decisions.create!(
        notebook: claim.notebook,
        decision: decision,
        note: required_note(note),
        authority: "user"
      )
    end

    private

    def required_note(note)
      text = note.to_s.strip
      raise Error.new("validation", "keputusan butuh catatan") if text.empty?

      text
    end
  end
end

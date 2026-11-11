class ReviewDecision < ApplicationRecord
  DECISIONS = %w[accepted rejected needs_evidence status_changed].freeze
  CLAIM_DECISIONS = %w[accepted rejected needs_evidence].freeze

  belongs_to :notebook
  belongs_to :claim, optional: true
  belongs_to :business_record, optional: true

  validates :decision, inclusion: { in: DECISIONS }
  validates :note, presence: true
  validates :authority, presence: true
  validate :target_present

  private

  def target_present
    return if claim_id.present? || business_record_id.present?

    errors.add(:base, "keputusan harus menempel pada klaim atau rekaman")
  end
end

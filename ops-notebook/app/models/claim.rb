class Claim < ApplicationRecord
  belongs_to :section
  belongs_to :document
  belongs_to :notebook
  has_many :review_decisions, dependent: :destroy

  scope :active, -> { where(state: "active") }

  def latest_review
    if review_decisions.loaded?
      review_decisions.max_by(&:id)
    else
      review_decisions.order(id: :desc).first
    end
  end

  def blocked?
    %w[rejected needs_evidence].include?(latest_review&.decision)
  end
end


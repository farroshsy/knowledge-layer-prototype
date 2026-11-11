class BusinessRecord < ApplicationRecord
  KINDS = %w[person work_item].freeze
  STATUSES = %w[unknown planned occurred].freeze

  belongs_to :notebook
  has_many :review_decisions, dependent: :destroy

  validates :kind, inclusion: { in: KINDS }
  validates :status, inclusion: { in: STATUSES }
  validates :display_name, presence: true
  validates :public_id, presence: true, uniqueness: true

  before_validation :assign_public_id, on: :create

  private

  def assign_public_id
    self.public_id ||= SecureRandom.hex(16)
  end
end

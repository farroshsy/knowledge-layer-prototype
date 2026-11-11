class Intake < ApplicationRecord
  belongs_to :notebook
  belongs_to :document, optional: true

  KINDS = %w[plain pdf image designed recording unknown].freeze
  ROUTES = %w[direct text_layer text_layer_or_ocr ocr chunk transcript reject].freeze
  STATUSES = %w[mapped blocked].freeze

  validates :filename, :physical_kind, :route, :status, :reason, presence: true
  validates :physical_kind, inclusion: { in: KINDS }
  validates :route, inclusion: { in: ROUTES }
  validates :status, inclusion: { in: STATUSES }
end
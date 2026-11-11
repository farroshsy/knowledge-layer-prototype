class ExtractedField < ApplicationRecord
  belongs_to :section
  belongs_to :document

  scope :active, -> { where(state: "active") }
end

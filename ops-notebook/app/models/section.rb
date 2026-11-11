class Section < ApplicationRecord
  belongs_to :document
  has_many :classifications, dependent: :destroy
  has_many :claims, dependent: :destroy
  has_many :extracted_fields, dependent: :destroy

  def active_classification
    rows = if classifications.loaded?
      classifications.select { |row| row.state == "active" }
    else
      classifications.where(state: "active").to_a
    end
    rows.max_by(&:generation)
  end

  def user_locked?
    classifications.where(state: "active", method: "user").exists?
  end
end

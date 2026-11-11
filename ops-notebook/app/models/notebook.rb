class Notebook < ApplicationRecord
  has_many :business_records, dependent: :destroy
  has_many :documents, dependent: :destroy
  has_many :intakes, dependent: :destroy
  has_many :claims, dependent: :destroy
  has_many :review_decisions, dependent: :destroy

  validates :name, presence: true
end

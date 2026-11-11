class Document < ApplicationRecord
  belongs_to :notebook
  has_many :sections, dependent: :destroy
  has_many :classifications, through: :sections
  has_many :jobs, dependent: :destroy
  has_many :claims, dependent: :destroy
  has_many :extracted_fields, dependent: :destroy

  validates :filename, presence: true
  validates :body, presence: true
  validates :content_hash, presence: true, uniqueness: { scope: :notebook_id }

  attr_accessor :reused_upload
end

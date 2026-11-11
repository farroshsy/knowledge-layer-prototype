class CreateReviewDecisions < ActiveRecord::Migration[7.0]
  def change
    create_table :review_decisions do |t|
      t.references :notebook, null: false, foreign_key: true
      t.references :claim, foreign_key: true
      t.references :business_record, foreign_key: true
      t.string :decision, null: false
      t.text :note, null: false
      t.string :authority, null: false, default: "user"
      t.string :previous_status
      t.string :next_status
      t.timestamps
    end
  end
end

class CreateIntakes < ActiveRecord::Migration[7.0]
  def change
    create_table :intakes do |t|
      t.references :notebook, null: false, foreign_key: true
      t.references :document, foreign_key: true
      t.string :filename, null: false
      t.integer :byte_size
      t.string :physical_kind, null: false
      t.string :route, null: false
      t.string :status, null: false
      t.text :reason, null: false
      t.timestamps
    end
  end
end
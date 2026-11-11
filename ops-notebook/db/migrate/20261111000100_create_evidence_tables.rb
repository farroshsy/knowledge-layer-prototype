class CreateEvidenceTables < ActiveRecord::Migration[7.0]
  def change
    create_table :notebooks do |t|
      t.string :name, null: false
      t.timestamps
    end

    create_table :business_records do |t|
      t.references :notebook, null: false, foreign_key: true
      t.string :public_id, null: false
      t.string :kind, null: false
      t.string :display_name, null: false
      t.string :status, null: false
      t.timestamps
    end
    add_index :business_records, :public_id, unique: true

    create_table :documents do |t|
      t.references :notebook, null: false, foreign_key: true
      t.string :filename, null: false
      t.text :body, null: false
      t.timestamps
    end

    create_table :sections do |t|
      t.references :document, null: false, foreign_key: true
      t.integer :ordinal, null: false
      t.text :body_text, null: false
      t.integer :start_offset, null: false
      t.integer :end_offset, null: false
      t.timestamps
    end

    create_table :classifications do |t|
      t.references :section, null: false, foreign_key: true
      t.string :category, null: false
      t.string :method, null: false
      t.text :reason, null: false
      t.string :state, null: false, default: "active"
      t.integer :generation, null: false
      t.timestamps
    end

    create_table :claims do |t|
      t.references :section, null: false, foreign_key: true
      t.references :document, null: false, foreign_key: true
      t.references :notebook, null: false, foreign_key: true
      t.text :quote, null: false
      t.integer :start_offset, null: false
      t.integer :end_offset, null: false
      t.string :polarity, null: false
      t.string :modality, null: false
      t.string :predicate, null: false, default: ""
      t.string :method, null: false
      t.string :state, null: false, default: "active"
      t.integer :generation, null: false
      t.timestamps
    end

    create_table :extracted_fields do |t|
      t.references :section, null: false, foreign_key: true
      t.references :document, null: false, foreign_key: true
      t.string :name, null: false
      t.text :value, null: false
      t.text :quote, null: false
      t.string :method, null: false
      t.string :state, null: false, default: "active"
      t.integer :generation, null: false
      t.timestamps
    end

    create_table :jobs do |t|
      t.references :document, null: false, foreign_key: true
      t.string :status, null: false
      t.integer :attempt, null: false, default: 1
      t.text :error
      t.string :provider_method
      t.string :provider_label
      t.text :provider_error
      t.timestamps
    end
  end
end

class AddContentHashToDocuments < ActiveRecord::Migration[7.0]
  def up
    add_column :documents, :content_hash, :string
    Document.reset_column_information
    seen = {}
    Document.find_each do |document|
      digest = Digest::SHA256.hexdigest(document.body.to_s)
      key = [document.notebook_id, digest]
      if seen[key]
        document.destroy!
      else
        document.update_columns(content_hash: digest)
        seen[key] = document.id
      end
    end
    change_column_null :documents, :content_hash, false
    add_index :documents, [:notebook_id, :content_hash], unique: true
  end

  def down
    remove_index :documents, [:notebook_id, :content_hash]
    remove_column :documents, :content_hash
  end
end

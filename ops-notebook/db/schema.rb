# This file is auto-generated from the current state of the database. Instead
# of editing this file, please use the migrations feature of Active Record to
# incrementally modify your database, and then regenerate this schema definition.
#
# This file is the source Rails uses to define your schema when running `bin/rails
# db:schema:load`. When creating a new database, `bin/rails db:schema:load` tends to
# be faster and is potentially less error prone than running all of your
# migrations from scratch. Old migrations may fail to apply correctly if those
# migrations use external dependencies or application code.
#
# It's strongly recommended that you check this file into your version control system.

ActiveRecord::Schema[7.0].define(version: 2026_11_11_023000) do
  # These are extensions that must be enabled in order to support this database
  enable_extension "plpgsql"

  create_table "business_records", force: :cascade do |t|
    t.bigint "notebook_id", null: false
    t.string "public_id", null: false
    t.string "kind", null: false
    t.string "display_name", null: false
    t.string "status", null: false
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["notebook_id"], name: "index_business_records_on_notebook_id"
    t.index ["public_id"], name: "index_business_records_on_public_id", unique: true
  end

  create_table "claims", force: :cascade do |t|
    t.bigint "section_id", null: false
    t.bigint "document_id", null: false
    t.bigint "notebook_id", null: false
    t.text "quote", null: false
    t.integer "start_offset", null: false
    t.integer "end_offset", null: false
    t.string "polarity", null: false
    t.string "modality", null: false
    t.string "predicate", default: "", null: false
    t.string "method", null: false
    t.string "state", default: "active", null: false
    t.integer "generation", null: false
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["document_id"], name: "index_claims_on_document_id"
    t.index ["notebook_id"], name: "index_claims_on_notebook_id"
    t.index ["section_id"], name: "index_claims_on_section_id"
  end

  create_table "classifications", force: :cascade do |t|
    t.bigint "section_id", null: false
    t.string "category", null: false
    t.string "method", null: false
    t.text "reason", null: false
    t.string "state", default: "active", null: false
    t.integer "generation", null: false
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["section_id"], name: "index_classifications_on_section_id"
  end

  create_table "documents", force: :cascade do |t|
    t.bigint "notebook_id", null: false
    t.string "filename", null: false
    t.text "body", null: false
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.string "content_hash", null: false
    t.index ["notebook_id", "content_hash"], name: "index_documents_on_notebook_id_and_content_hash", unique: true
    t.index ["notebook_id"], name: "index_documents_on_notebook_id"
  end

  create_table "extracted_fields", force: :cascade do |t|
    t.bigint "section_id", null: false
    t.bigint "document_id", null: false
    t.string "name", null: false
    t.text "value", null: false
    t.text "quote", null: false
    t.string "method", null: false
    t.string "state", default: "active", null: false
    t.integer "generation", null: false
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["document_id"], name: "index_extracted_fields_on_document_id"
    t.index ["section_id"], name: "index_extracted_fields_on_section_id"
  end

  create_table "intakes", force: :cascade do |t|
    t.bigint "notebook_id", null: false
    t.bigint "document_id"
    t.string "filename", null: false
    t.integer "byte_size"
    t.string "physical_kind", null: false
    t.string "route", null: false
    t.string "status", null: false
    t.text "reason", null: false
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["document_id"], name: "index_intakes_on_document_id"
    t.index ["notebook_id"], name: "index_intakes_on_notebook_id"
  end

  create_table "jobs", force: :cascade do |t|
    t.bigint "document_id", null: false
    t.string "status", null: false
    t.integer "attempt", default: 1, null: false
    t.text "error"
    t.string "provider_method"
    t.string "provider_label"
    t.text "provider_error"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["document_id"], name: "index_jobs_on_document_id"
  end

  create_table "notebooks", force: :cascade do |t|
    t.string "name", null: false
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
  end

  create_table "review_decisions", force: :cascade do |t|
    t.bigint "notebook_id", null: false
    t.bigint "claim_id"
    t.bigint "business_record_id"
    t.string "decision", null: false
    t.text "note", null: false
    t.string "authority", default: "user", null: false
    t.string "previous_status"
    t.string "next_status"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["business_record_id"], name: "index_review_decisions_on_business_record_id"
    t.index ["claim_id"], name: "index_review_decisions_on_claim_id"
    t.index ["notebook_id"], name: "index_review_decisions_on_notebook_id"
  end

  create_table "sections", force: :cascade do |t|
    t.bigint "document_id", null: false
    t.integer "ordinal", null: false
    t.text "body_text", null: false
    t.integer "start_offset", null: false
    t.integer "end_offset", null: false
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["document_id"], name: "index_sections_on_document_id"
  end

  add_foreign_key "business_records", "notebooks"
  add_foreign_key "claims", "documents"
  add_foreign_key "claims", "notebooks"
  add_foreign_key "claims", "sections"
  add_foreign_key "classifications", "sections"
  add_foreign_key "documents", "notebooks"
  add_foreign_key "extracted_fields", "documents"
  add_foreign_key "extracted_fields", "sections"
  add_foreign_key "intakes", "documents"
  add_foreign_key "intakes", "notebooks"
  add_foreign_key "jobs", "documents"
  add_foreign_key "review_decisions", "business_records"
  add_foreign_key "review_decisions", "claims"
  add_foreign_key "review_decisions", "notebooks"
  add_foreign_key "sections", "documents"
end

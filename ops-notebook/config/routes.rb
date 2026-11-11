Rails.application.routes.draw do
  root "workbench#show"
  get "riset", to: "workbench#riset", as: :riset
  get "handoff", to: "workbench#handoff", as: :handoff
  post "notebooks", to: "workbench#create_notebook"
  post "notebooks/example", to: "workbench#create_example", as: :example_notebooks
  post "notebooks/:notebook_id/records", to: "workbench#create_record", as: :notebook_records
  post "notebooks/:notebook_id/documents", to: "workbench#create_document", as: :notebook_documents
  get "notebooks/:notebook_id/pemetaan", to: "workbench#pemetaan", as: :notebook_pemetaan
  get "notebooks/:notebook_id/proses", to: "workbench#proses", as: :notebook_proses
  get "notebooks/:notebook_id/analisis", to: "workbench#analisis", as: :notebook_analisis
  get "notebooks/:notebook_id/keputusan", to: "workbench#keputusan", as: :notebook_keputusan
  get "notebooks/:notebook_id/verifikasi", to: "workbench#verifikasi", as: :notebook_verifikasi
  get "notebooks/:notebook_id/tanya", to: "workbench#tanya", as: :notebook_tanya
  post "sections/:id/correction", to: "workbench#correct_section", as: :section_correction
  post "documents/:id/reprocess", to: "workbench#reprocess_document", as: :reprocess_document
  post "notebooks/:notebook_id/query", to: "workbench#query", as: :notebook_query
  post "records/:id/status", to: "workbench#change_status", as: :record_status
  post "claims/:id/decision", to: "workbench#decide_claim", as: :claim_decision
end

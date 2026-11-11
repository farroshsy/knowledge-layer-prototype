class Notebook::Board
  attr_reader :records, :work_items, :people, :documents, :claims, :decisions, :conflicts, :intakes

  def initialize(notebook)
    @records = notebook.business_records.order(:id).to_a
    @work_items = @records.select { |record| record.kind == "work_item" }
    @people = @records.select { |record| record.kind == "person" }
    @documents = notebook.documents.includes(:jobs, sections: [:classifications, :extracted_fields], claims: :review_decisions).order(:id).to_a
    @claims = notebook.claims.active.includes(:review_decisions, :document, :section).order(:id).to_a
    @decisions = notebook.review_decisions.includes(:business_record, :claim).order(id: :desc).limit(8).to_a
    @conflicts = Evidence.conflicts(@claims)
    @intakes = notebook.intakes.order(:id).to_a
  end
end

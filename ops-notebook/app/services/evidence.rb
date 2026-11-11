module Evidence
  class Error < StandardError
    attr_reader :code

    def initialize(code, message)
      @code = code
      super(message)
    end
  end

  Result = Struct.new(
    :route, :answer, :reason, :method, :semantic, :records, :claims, :rows,
    keyword_init: true
  )
  CATEGORIES = Lexicon::CATEGORIES

  def self.upload(notebook, filename, body) = Ingest.upload(notebook, filename, body)
  def self.receive(notebook, filename, body = "", byte_size: nil) = Ingest.receive(notebook, filename, body, byte_size: byte_size)
  def self.correct(section, category) = Ingest.correct(section, category)
  def self.reprocess(document) = Ingest.reprocess(document)
  def self.ask(notebook, question) = Query.ask(notebook, question)
  def self.change_status(record, status, note) = Review.change_status(record, status, note)
  def self.decide_claim(claim, decision, note) = Review.decide_claim(claim, decision, note)
  def self.conflicts(claims) = Query.conflicts(claims)
  def self.load_demo_fixtures(notebook) = Ingest.load_demo_fixtures(notebook)
end

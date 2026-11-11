class WorkbenchController < ApplicationController
  layout "workbench"
  def show
    load_notebook
    return unless @notebook

    case params[:langkah].to_i
    when 2 then redirect_to notebook_proses_path(@notebook)
    when 3 then redirect_to notebook_tanya_path(@notebook)
    end
  end

  def pemetaan
    prepare_notebook or return
  end

  def proses
    prepare_notebook or return
  end

  def analisis
    prepare_notebook or return
  end

  def keputusan
    prepare_notebook or return
  end

  def verifikasi
    prepare_notebook or return
  end

  def tanya
    prepare_notebook or return
  end

  def create_notebook
    notebook = Notebook.create!(name: params[:name].to_s.strip.presence || "Operasional")
    redirect_to root_path(notebook_id: notebook.id)
  rescue ActiveRecord::RecordInvalid => error
    redirect_to root_path, alert: error.record.errors.full_messages.to_sentence
  end

  def create_example
    notebook = SampleWorkspace.create!
    redirect_to root_path(notebook_id: notebook.id), notice: "Contoh produk siap dipakai."
  rescue Evidence::Error, ActiveRecord::RecordInvalid => error
    redirect_to root_path, alert: error.message
  end

  def create_record
    notebook = Notebook.find(params[:notebook_id])
    notebook.business_records.create!(
      kind: params[:kind],
      display_name: params[:display_name].to_s.strip,
      status: params[:status]
    )
    redirect_to root_path(notebook_id: notebook.id, langkah: 1)
  rescue ActiveRecord::RecordInvalid, ActiveRecord::RecordNotFound => error
    redirect_to root_path(notebook_id: params[:notebook_id], langkah: 1), alert: error.message
  end

  def create_document
    notebook = Notebook.find(params[:notebook_id])
    items = upload_items
    raise Evidence::Error.new("validation", "tidak ada berkas") if items.empty?

    intakes = items.map { |filename, body, byte_size| Evidence.receive(notebook, filename, body, byte_size: byte_size) }
    reused = intakes.count { |row| row.document&.reused_upload }
    mapped = intakes.count { |row| row.status == "mapped" } - reused
    blocked = intakes.count { |row| row.status == "blocked" }
    notice = if blocked.positive?
      "#{mapped} berkas teks dipetakan. #{blocked} berkas ditahan sebelum OCR, lapisan teks, atau pemotongan."
    elsif items.one? && params[:batch].blank?
      reused.positive? ? "Teks yang sama sudah tersimpan." : "Berkas masuk. Periksa jenisnya."
    else
      "#{mapped} berkas masuk. #{reused} teks yang sama sudah tersimpan."
    end
    target = blocked.positive? ? notebook_pemetaan_path(notebook) : notebook_proses_path(notebook)
    redirect_to target, notice: notice
  rescue Evidence::Error, ActiveRecord::RecordNotFound => error
    redirect_to root_path(notebook_id: params[:notebook_id], langkah: 1), alert: error.message
  end

  def correct_section
    section = Section.find(params[:id])
    Evidence.correct(section, params[:category].to_s)
    redirect_to notebook_analisis_path(section.document.notebook_id, berkas: section.document_id), notice: "Jenis berkas diperbarui."
  rescue Evidence::Error, ActiveRecord::RecordNotFound => error
    redirect_to root_path, alert: error.message
  end

  def reprocess_document
    document = Document.find(params[:id])
    Evidence.reprocess(document)
    redirect_to notebook_analisis_path(document.notebook_id, berkas: document.id)
  rescue ActiveRecord::RecordNotFound => error
    redirect_to root_path, alert: error.message
  end

  def change_status
    record = BusinessRecord.find(params[:id])
    Evidence.change_status(record, params[:status].to_s, params[:note].to_s)
    redirect_to root_path(notebook_id: record.notebook_id, langkah: 1), notice: "Status tercatat."
  rescue Evidence::Error => error
    redirect_to root_path(notebook_id: record.notebook_id, langkah: 1), alert: error.message
  rescue ActiveRecord::RecordNotFound => error
    redirect_to root_path, alert: error.message
  end

  def decide_claim
    claim = Claim.find(params[:id])
    Evidence.decide_claim(claim, params[:decision].to_s, params[:note].to_s)
    redirect_to notebook_verifikasi_path(claim.notebook_id, berkas: claim.document_id), notice: "Tinjauan tersimpan."
  rescue Evidence::Error => error
    redirect_to notebook_verifikasi_path(claim.notebook_id, berkas: claim.document_id), alert: error.message
  rescue ActiveRecord::RecordNotFound => error
    redirect_to root_path, alert: error.message
  end

  def query
    notebook = Notebook.find(params[:notebook_id])
    result = Evidence.ask(notebook, params[:question].to_s)
    load_board(notebook)
    @notebook = notebook
    @result = result
    @question = params[:question].to_s
    render :tanya
  rescue Evidence::Error, ActiveRecord::RecordNotFound => error
    redirect_to notebook_tanya_path(params[:notebook_id]), alert: error.message
  end

  private

  def upload_items
    raw = params[:batch].to_s
    return [[params[:filename].to_s, params[:body].to_s, params[:byte_size]]] if raw.blank?

    rows = JSON.parse(raw)
    raise Evidence::Error.new("validation", "daftar berkas tidak terbaca") unless rows.is_a?(Array)

    rows.filter_map do |row|
      filename = row["filename"].to_s
      body = row["encoding"] == "base64" ? Base64.decode64(row["body"].to_s) : row["body"].to_s
      next if filename.blank? && body.blank?

      [filename, body, row["byte_size"]]
    end
  rescue JSON::ParserError
    raise Evidence::Error.new("validation", "daftar berkas tidak terbaca")
  end

  def prepare_notebook
    @notebook = Notebook.find(params[:notebook_id])
    load_board(@notebook)
    true
  rescue ActiveRecord::RecordNotFound
    redirect_to root_path, alert: "Ruang tidak ditemukan."
    false
  end

  def load_notebook
    @notebooks = Notebook.order(:id)
    @notebook = Notebook.find_by(id: params[:notebook_id]) || @notebooks.last
    load_board(@notebook) if @notebook
  end

  def load_board(notebook)
    board = Notebook::Board.new(notebook)
    @records = board.records
    @work_items = board.work_items
    @people = board.people
    @documents = board.documents
    @claims = board.claims
    @decisions = board.decisions
    @conflicts = board.conflicts
    @intakes = board.intakes
  end
end

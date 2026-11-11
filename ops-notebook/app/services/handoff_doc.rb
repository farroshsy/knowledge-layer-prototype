# Renders HANDOFF.md for the screen. The Markdown file stays the only copy.
class HandoffDoc
  PATH = Rails.root.join("..", "HANDOFF.md")

  def self.html
    raise Errno::ENOENT, PATH.to_s unless PATH.file?

    blocks(PATH.read).join("\n")
  end

  def self.blocks(markdown)
    lines = markdown.lines.map { |line| line.delete_suffix("\n") }
    out = []
    index = 0
    while index < lines.length
      line = lines[index]
      if line.start_with?("```")
        index += 1
        body = []
        while index < lines.length && !lines[index].start_with?("```")
          body << lines[index]
          index += 1
        end
        index += 1
        out << "<pre><code>#{escape(body.join("\n"))}</code></pre>"
      elsif line.start_with?("|")
        rows = []
        while index < lines.length && lines[index].start_with?("|")
          rows << lines[index]
          index += 1
        end
        out << table(rows)
      elsif line.match?(/\A- /)
        items = []
        while index < lines.length && lines[index].match?(/\A- /)
          items << lines[index].delete_prefix("- ")
          index += 1
        end
        out << "<ul>#{items.map { |item| "<li>#{inline(item)}</li>" }.join}</ul>"
      elsif line.match?(/\A\d+\. /)
        items = []
        while index < lines.length && lines[index].match?(/\A\d+\. /)
          items << lines[index].sub(/\A\d+\. /, "")
          index += 1
        end
        out << "<ol>#{items.map { |item| "<li>#{inline(item)}</li>" }.join}</ol>"
      elsif line.start_with?("### ")
        text = line.delete_prefix("### ")
        out << %(<h3 id="#{anchor(text)}">#{inline(text)}</h3>)
        index += 1
      elsif line.start_with?("## ")
        text = line.delete_prefix("## ")
        out << %(<h2 id="#{anchor(text)}">#{inline(text)}</h2>)
        index += 1
      elsif line.start_with?("# ")
        text = line.delete_prefix("# ")
        out << %(<h1 id="#{anchor(text)}">#{inline(text)}</h1>)
        index += 1
      elsif line.strip.empty?
        index += 1
      else
        paragraph = [line]
        index += 1
        while index < lines.length && lines[index].strip != "" && !structural?(lines[index])
          paragraph << lines[index]
          index += 1
        end
        out << "<p>#{inline(paragraph.join(" "))}</p>"
      end
    end
    out
  end

  def self.structural?(line)
    line.start_with?("#", "|", "```", "- ") || line.match?(/\A\d+\. /)
  end

  def self.table(rows)
    cells = rows.reject { |row| row.match?(/\A\|(?:\s*:?-+:?\s*\|)+\z/) }.map do |row|
      row.split("|")[1..-2].to_a.map { |cell| inline(cell.strip) }
    end
    return "" if cells.empty?

    head = cells.first.map { |cell| "<th>#{cell}</th>" }.join
    body = cells.drop(1).map { |row| "<tr>#{row.map { |cell| "<td>#{cell}</td>" }.join}</tr>" }.join
    "<div class=\"compare\"><table><thead><tr>#{head}</tr></thead><tbody>#{body}</tbody></table></div>"
  end

  def self.inline(text)
    escaped = escape(text)
    escaped = escaped.gsub(/\[(.+?)\]\((.+?)\)/, '<a href="\2">\1</a>')
    escaped = escaped.gsub(/`([^`]+)`/, '<code>\1</code>')
    escaped.gsub(/\*\*(.+?)\*\*/, "<strong>\\1</strong>")
  end

  def self.anchor(text)
    text.downcase.gsub(/[^\p{Alnum}\s-]/, "").strip.gsub(/\s+/, "-")
  end

  def self.escape(text)
    ERB::Util.html_escape(text)
  end

  private_class_method :blocks, :structural?, :table, :inline, :anchor, :escape
end

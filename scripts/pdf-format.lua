-- PDF-only structure: chapter breaks, reference panels and numbered cross-links.
function Pandoc(doc)
  local blocks, references = pandoc.List(), nil
  local skip_reading, chapter_seen = false, false
  local counters, numbers = {0, 0, 0, 0, 0, 0}, {}

  local function close_references()
    if references then
      blocks:insert(pandoc.RawBlock("latex", "\\begin{reportreferences}"))
      blocks:extend(references)
      blocks:insert(pandoc.RawBlock("latex", "\\end{reportreferences}"))
      references = nil
    end
  end

  for _, block in ipairs(doc.blocks) do
    if block.t == "Header" then
      close_references()
      skip_reading = pandoc.utils.stringify(block.content) == "Further reading"
      if not skip_reading then
        if pandoc.utils.stringify(block.content) == "References" then
          block.classes:insert("unnumbered")
          block.classes:insert("unlisted")
          references = pandoc.List()
        else
          local level = block.level
          counters[level] = counters[level] + 1
          for i = level + 1, 6 do counters[i] = 0 end
          local parts = {}
          for i = 1, math.min(level, 3) do parts[i] = tostring(counters[i]) end
          numbers[block.identifier] = table.concat(parts, ".")
          if level == 1 then
            if chapter_seen then blocks:insert(pandoc.RawBlock("latex", "\\clearpage")) end
            chapter_seen = true
          end
        end
      end
    end
    if not skip_reading then
      if references then references:insert(block) else blocks:insert(block) end
    end
  end
  close_references()
  doc.blocks = blocks
  return doc:walk({Link = function(link)
    if link.target:sub(1, 1) == "#" then
      local number = numbers[link.target:sub(2)]
      if number then
        link.content:insert(pandoc.Str(" (section " .. number .. ")"))
      end
    end
    return link
  end})
end

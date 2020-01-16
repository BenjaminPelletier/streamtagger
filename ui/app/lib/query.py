def get_where_clauses(args, transaction, userids_by_name):
  tagreqs = args.getlist('hastag')
  if tagreqs:
    tagdefs = transaction.get_tag_definitions()
    where_clauses = []
    for tagreq in tagreqs:
      tagexprs = tagreq.split('|')
      or_clauses = []
      for tagexpr in tagexprs:
        if '=' in tagexpr:
          tagexpr, tagvalue = tagexpr.split('=')
          tagvalue = int(tagvalue)
        else:
          tagvalue = None
        if '@' in tagexpr:
          tagusername, tagname = tagexpr.split('@')
        else:
          tagusername, tagname = None, tagexpr
        or_clause = 'tags.tag_id = \'%s\'' % tagdefs[tagname].id
        if tagusername:
          or_clause += ' AND tags.user_id = \'%s\'' % userids_by_name[
            tagusername]
        if tagvalue:
          or_clause += ' AND tags.value = %d' % tagvalue
        or_clauses.append('(' + or_clause + ')')
      if len(or_clauses) > 1:
        where_clauses.append('(' + ' OR '.join(or_clauses) + ')')
      else:
        where_clauses.append(or_clauses[0])
    return where_clauses
  else:
    return None

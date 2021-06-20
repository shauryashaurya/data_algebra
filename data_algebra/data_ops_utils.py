import data_algebra.expr_rep


def try_to_merge_ops(ops1, ops2):
    ops1_columns_used = set(data_algebra.expr_rep.get_columns_used(ops1))
    ops1_columns_produced = set([k for k in ops1.keys()])
    ops2_columns_used = set(data_algebra.expr_rep.get_columns_used(ops2))
    ops2_columns_produced = set([k for k in ops2.keys()])
    common_produced = ops1_columns_produced.intersection(ops2_columns_produced)
    if len(common_produced) > 0:
        ops1_common = {k: ops1[k] for k in common_produced}
        ops2_common = {k: ops2[k] for k in common_produced}
        ops1_common_columns_used = set(
            data_algebra.expr_rep.get_columns_used(ops1_common)
        )
        ops1_common_columns_produced = set([k for k in ops1_common.keys()])
        ops2_common_columns_used = set(
            data_algebra.expr_rep.get_columns_used(ops2_common)
        )
        ops2_common_columns_produced = set([k for k in ops2_common.keys()])
        if len(ops1_common_columns_used.intersection(ops2_columns_produced)) > 0:
            return None
        if len(ops1_common_columns_used.intersection(ops1_columns_produced)) > 0:
            return None
        if len(ops2_common_columns_used.intersection(ops1_columns_produced)) > 0:
            return None
        if len(ops2_common_columns_used.intersection(ops2_columns_produced)) > 0:
            return None
        new_ops = {k: ops1[k] for k in ops1.keys() if k not in common_produced}
        new_ops.update(ops2)
        return new_ops
    # check required disjointness conditions
    if len(ops1_columns_produced.intersection(ops2_columns_produced)) > 0:
        return None
    if len(ops1_columns_used.intersection(ops2_columns_produced)) > 0:
        return None
    if len(ops2_columns_used.intersection(ops1_columns_produced)) > 0:
        return None
    # all of ops1 must have the same view
    views1 = list()
    for v in ops1.values():
        for vi in v.get_views():
            if vi not in views1:  # expect list to be of size zero or one
                views1.append(vi)
    views2 = list()
    for v in ops2.values():
        for vi in v.get_views():
            if vi not in views2:  # expect list to be of size zero or one
                views2.append(vi)
    if len(views1) > 1:
        return None
    if len(views2) > 1:
        return None
    # merge the extends
    new_ops = ops1.copy()
    new_ops2 = ops2
    if (len(views1) > 0) and (len(views2) > 0):
        new_ops2 = {k: v.replace_view(views1[0]) for k, v in ops2.items()}
    new_ops.update(new_ops2)
    return new_ops

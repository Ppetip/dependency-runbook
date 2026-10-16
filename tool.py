"""Compute deterministic recovery order and parallelizable stages for service dependencies, rejecting cycles and missing references."""
def analyze(data):
    graph = {name:set(deps) for name,deps in data['services'].items()}
    unknown = set().union(*graph.values())-graph.keys() if graph else set()
    if unknown:
        raise ValueError('unknown dependencies: '+', '.join(sorted(unknown)))
    done = set()
    result = []
    while len(done)<len(graph):
        ready = sorted(name for name,deps in graph.items() if name not in done and deps<=done)
        if not ready:
            blocked = sorted(set(graph)-done)
            raise ValueError('dependency cycle blocks: '+', '.join(blocked))
        result.append(dict(kind='stage',stage=len(result)+1,services=ready))
        done.update(ready)
    return result


def main():
    import argparse, json, sys
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', help='path to JSON input, or - for stdin')
    args = parser.parse_args()
    try:
        if args.input == '-':
            data = json.load(sys.stdin)
        else:
            with open(args.input, encoding='utf-8') as stream:
                data = json.load(stream)
        result = analyze(data)
        print(json.dumps(result, indent=2, allow_nan=False))
        return 0
    except (ValueError, KeyError, TypeError, OSError, OverflowError) as error:
        print('Invalid input: '+str(error), file=sys.stderr)
        return 2

if __name__ == '__main__':
    raise SystemExit(main())

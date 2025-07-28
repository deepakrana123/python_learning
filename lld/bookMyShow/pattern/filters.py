class FilterStrategy:
    def apply(self, value, shows):
        raise NotImplementedError


class CityFilter(FilterStrategy):
    def apply(self, value, shows):
        return [s for s in shows if s.theatre.get_city() == value.lower()]


class MovieFilter(FilterStrategy):
    def apply(self, value, shows):
        return [s for s in shows if s.movie.get_title().lower() == value.lower()]


class FilterContext:
    _filters = {"city": CityFilter(), "movie": MovieFilter()}

    def apply_filter(self, filter_type, value, shows):
        return self._filters.get(filter_type, CityFilter()).apply(value, shows)

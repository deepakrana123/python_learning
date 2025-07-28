from pattern.filters import FilterContext


class ViewManager:
    @staticmethod
    def show_movies(movies):
        for idx, movie in enumerate(movies):
            print(f"{idx} {movie.title}")

    @staticmethod
    def show_shows(shows):
        for idx, show in enumerate(shows):
            print(f"{idx} {show.title}")

    @staticmethod
    def filter_shows(shows, filter_type, filter_value):
        print(f"\n🔍 Filtered by {filter_type} = {filter_value}")
        filter_context = FilterContext()
        filtered = filter_context.apply_filter(filter_type, filter_value, shows)
        ViewManager.show_shows(filtered)
        return filtered

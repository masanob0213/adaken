import { ref, onMounted } from "vue";
import axios from "axios";

export function useMainScript() {
  const works = ref([]);
  const title = ref("");

  const fetchWorks = async (titleParam) => {
    const baseUrl = import.meta.env.VITE_API_BASE_URL;
    const url = baseUrl + "/api/v1/works/";
    const params = {};

    if (title.value) {
      params.title = title.value;
    }

    params.limit = 10;

    console.log("jajcnjka");

    try {
      const res = await axios.get(url, { params });
      works.value = res.data;
      console.log(works.value);
    } catch (err) {
      console.error("取得失敗:", err);
    }
  };

  onMounted(async () => {
    await fetchWorks();
  });

  return {
    title,
    works,
    fetchWorks,
  };
}

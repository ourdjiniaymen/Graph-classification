import { createRoot } from "react-dom/client";
import { store } from "./framework/presentation/store/store";
import { Provider } from "react-redux";
import App from "./App";
import "./index.css"
const container: HTMLElement | null = document.getElementById("root");
const root = createRoot(container as Element);
root.render(
  <Provider store={store}>
    <App />
  </Provider>
);

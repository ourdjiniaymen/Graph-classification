import { configureStore } from "@reduxjs/toolkit";
import KernelSlice from "../viewmodel/slices/KernelSlice";
import DataSetSlice from "../viewmodel/slices/DataSetSlice";
import ResultlSlice from "../viewmodel/slices/ResultSlice";
import ClassificationSlice from "../viewmodel/slices/ClassificationSlice";

export const store = configureStore({
  reducer: { KernelSlice, DataSetSlice, ResultlSlice, ClassificationSlice },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;

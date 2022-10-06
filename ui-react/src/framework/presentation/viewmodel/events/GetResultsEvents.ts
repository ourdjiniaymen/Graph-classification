import { createAsyncThunk, PayloadAction } from "@reduxjs/toolkit";
import Result from "../../../../business/domain/Result";
import di from "../../../../di";
import { ResultState } from "../slices/ResultSlice";

export const GetResultsEvents = () => {
  const getResultsEvent = createAsyncThunk(
    "result/getResultsEvent",
    async (_, thunkAPI) => {
      const { dispatch } = thunkAPI;
      dispatch(di.GetResultsUseCase.getResults());
    }
  );

  const handlePending = (state: ResultState) => {
    state.isLoadingResult = true;
    state.error = null;
  };

  const handleFulfilled = (
    state: ResultState,
    action: PayloadAction<Result[]>
  ) => {
    state.isLoadingResult = false;
    state.results = action.payload;
  };

  const handleRejected = (
    state: ResultState,
    action: PayloadAction<unknown>
  ) => {
    state.isLoadingResult = false;
    state.error = action.payload as string;
  };
  return {
    getResultsEvent,
    handlePending,
    handleFulfilled,
    handleRejected,
  };
};

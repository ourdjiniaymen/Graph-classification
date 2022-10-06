import di from "../../../../di";
import { createSlice } from "@reduxjs/toolkit";
import Result from "../../../../business/domain/Result";
import { GetResultsEvents } from "../events/GetResultsEvents";

export interface ResultState {
  results: Result[];
  isLoadingResult: boolean;
  error: string | null;
}

const initState: ResultState = {
  results: [],
  isLoadingResult: false,
  error: null,
};

const resultlSlice = createSlice({
  name: "result",
  initialState: initState,
  reducers: {},
  extraReducers: (builder) => {
    //get results
    builder.addCase(
      di.GetResultsUseCase.getResults.pending,
      GetResultsEvents().handlePending
    );
    builder.addCase(
      di.GetResultsUseCase.getResults.fulfilled,
      GetResultsEvents().handleFulfilled
    );
    builder.addCase(
      di.GetResultsUseCase.getResults.rejected,
      GetResultsEvents().handleRejected
    );
  },
});

export default resultlSlice.reducer;

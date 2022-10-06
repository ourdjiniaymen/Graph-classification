import di from "../../../../di";
import { createSlice } from "@reduxjs/toolkit";
import Result from "../../../../business/domain/Result";
import { RunClassificationEvents } from "../events/RunClassificationEvents";

export interface ClassificationState {
  result: Result | null;
  isLoadingClassification: boolean;
  error: string | null;
}

const initState: ClassificationState = {
  result: null,
  isLoadingClassification: false,
  error: null,
};

const classificationSlice = createSlice({
  name: "classification",
  initialState: initState,
  reducers: { resetResultEvent: RunClassificationEvents().resetResult },
  extraReducers: (builder) => {
    //get classification result
    builder.addCase(
      di.RunClassificationUseCase.runClassification.pending,
      RunClassificationEvents().handlePending
    );
    builder.addCase(
      di.RunClassificationUseCase.runClassification.fulfilled,
      RunClassificationEvents().handleFulfilled
    );
    builder.addCase(
      di.RunClassificationUseCase.runClassification.rejected,
      RunClassificationEvents().handleRejected
    );
  },
});

export const { resetResultEvent } = classificationSlice.actions;
export default classificationSlice.reducer;

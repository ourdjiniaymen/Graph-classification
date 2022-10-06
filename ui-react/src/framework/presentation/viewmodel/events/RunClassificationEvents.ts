import { createAsyncThunk, PayloadAction } from "@reduxjs/toolkit";
import Result from "../../../../business/domain/Result";
import RunClassification from "../../../../business/domain/RunClassification";
import di from "../../../../di";
import { ClassificationState } from "../slices/ClassificationSlice";

export const RunClassificationEvents = () => {
  const runClassificationEvent = createAsyncThunk(
    "classification/runClassificationEvent",
    async (runClassificationData: RunClassification, thunkAPI) => {
      const { dispatch } = thunkAPI;
      dispatch(
        di.RunClassificationUseCase.runClassification(runClassificationData)
      );
    }
  );

  const handlePending = (state: ClassificationState) => {
    state.isLoadingClassification = true;
    state.error = null;
  };

  const handleFulfilled = (
    state: ClassificationState,
    action: PayloadAction<Result>
  ) => {
    state.isLoadingClassification = false;
    state.result = action.payload;
  };

  const handleRejected = (
    state: ClassificationState,
    action: PayloadAction<unknown>
  ) => {
    state.isLoadingClassification = false;
    state.error = action.payload as string;
  };

  const resetResult = (state: ClassificationState) => {
    state.result = null;
  };

  return {
    runClassificationEvent,
    handlePending,
    handleFulfilled,
    handleRejected,
    resetResult,
  };
};

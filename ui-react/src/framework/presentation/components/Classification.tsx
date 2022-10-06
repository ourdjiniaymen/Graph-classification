import React, { useState, useEffect, ChangeEventHandler } from "react";
import { SelectChangeEvent } from "@mui/material/Select";
import DropSelect from "./DropSelect";
import MultipleSelectChip from "./MultipleSelectChip";
import { Grid } from "@mui/material";
import { useAppDispatch, useAppSelector } from "../store/hooks";
import { GetKernelsEvents } from "../viewmodel/events/GetKernelsEvents";
import { toSelectOptionKernel } from "../../../business/domain/Kernel";
import CircularProgressPage from "./CircularProgressPage";
import { GetDataSetsEvents } from "../viewmodel/events/GetDataSetsEvents";
import { toSelectOptionDataSet } from "../../../business/domain/DataSet";
import { cOptions, sigmaOptions } from "../utils/Constants";
import NumberField from "./NumberField";
import Checkbox from "@mui/material/Checkbox";
import Box from "@mui/material/Box";
import FormControlLabel from "@mui/material/FormControlLabel";
import Button from "@mui/material/Button";
import RunClassification from "../../../business/domain/RunClassification";
import { RunClassificationEvents } from "../viewmodel/events/RunClassificationEvents";
import ResultDialog from "./ResultDialog";
import { resetResultEvent } from "../viewmodel/slices/ClassificationSlice";

export const useSelectMultiple = (initialValue: string[]) => {
  const [value, setValue] = useState(initialValue);
  return [
    value,
    (event: SelectChangeEvent<string[]>) => {
      const {
        target: { value },
      } = event;
      setValue(
        // On autofill we get a stringified value.
        typeof value === "string" ? value.split(",") : value
      );
    },
    () => setValue([]),
  ] as const;
};

export const useSelectInput = (initialValue: string) => {
  const [value, setValue] = useState(initialValue);
  return [
    value,
    (
      event:
        | SelectChangeEvent
        | React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
    ) => {
      setValue(event.target.value);
    },
  ] as const;
};

export const useSelectCheckBox = (initialValue: boolean) => {
  const [value, setValue] = useState(initialValue);
  return [
    value,
    (event: React.ChangeEvent<HTMLInputElement>) => {
      setValue(event.target.checked);
    },
  ] as const;
};

const Classification = () => {
  const { isLoadingKernel, kernels } = useAppSelector(
    (state) => state.KernelSlice
  );
  const { isLoadingDataSet, dataSets } = useAppSelector(
    (state) => state.DataSetSlice
  );
  const { isLoadingClassification, result } = useAppSelector(
    (state) => state.ClassificationSlice
  );

  const dispatch = useAppDispatch();

  useEffect(() => {
    dispatch(GetKernelsEvents().getKernelsEvent());
    dispatch(GetDataSetsEvents().getDataSetsEvent());
  }, [dispatch]);

  const [kernel, handleKernel] = useSelectInput("");
  const [dataSet, handleDataSet] = useSelectInput("");
  const [sigma, handleSigma] = useSelectMultiple([]);
  const [c, handleC] = useSelectMultiple([]);
  const [cv, handleCv] = useSelectInput("");
  const [experiments, handleExperiments] = useSelectInput("");
  const [rbf, handleRbf] = useSelectCheckBox(false);
  const [normalize, handleNormalize] = useSelectCheckBox(false);
  const [withLabels, handleWithLabels] = useSelectCheckBox(false);
  const [withAttributes, handleWithAttributes] = useSelectCheckBox(false);
  const [parameters, handleParameters, resetParameters] = useSelectMultiple([]);
  const [kernelOptions, setKernelOptions] = useState<string[] | undefined>([]);

  const [openDialog, setOpenDialog] = useState<boolean>(false);
  const handleClose = () => {
    setOpenDialog(false);
    dispatch(resetResultEvent());
  };

  useEffect(() => {
    if (result != null) {
      console.log("result")
      console.log(result)
      setOpenDialog(true);
    }
  }, [result]);

  useEffect(() => {
    resetParameters();
    const selectedKernel = kernels.find((element) => element.name == kernel);
    setKernelOptions(
      selectedKernel?.parametersDetail
        .map((parameter) =>
          parameter.values.map((value) => parameter.name + " - " + value)
        )
        .reduce((accumulator, value) => accumulator.concat(value), [])
    );
  }, [kernel]);

  const handleRunClassification = () => {
    const parametersMap = new Map<string, number[]>();
    parameters.map((parameter) => {
      const splited = parameter.split(" - ");
      if (!parametersMap.has(splited[0])) {
        parametersMap.set(splited[0], [+splited[1]]);
      } else {
        const list = parametersMap.get(splited[0]) as number[];
        list.push(+splited[1]);
        parametersMap.set(splited[0], list);
      }
    });
    const parametersResult: {
      name: string;
      values: number[];
    }[] = [];
    for (const [key, value] of parametersMap) {
      parametersResult.push({ name: key, values: value });
    }

    const runClassification: RunClassification = {
      kernel: kernel,
      dataset: dataSet,
      rbf: rbf,
      sigma: sigma.map((element) => +element),
      normalize: normalize,
      c: c.map((element) => +element),
      cv: +cv,
      experiments: +experiments,
      with_labels: withLabels,
      with_attributes: withAttributes,
      parameters: parametersResult,
    };
    
    dispatch(
      RunClassificationEvents().runClassificationEvent(runClassification)
    );
  };

  return (
    <div>
      {result != null ? (
        <ResultDialog
          open={openDialog}
          handleClose={handleClose}
          result={result}
        />
      ) : (
        <div />
      )}

      {isLoadingKernel || isLoadingDataSet || isLoadingClassification ? (
        <CircularProgressPage
          isLoading={
            isLoadingKernel || isLoadingDataSet || isLoadingClassification
          }
        />
      ) : (
        <Grid
          container
          spacing={0}
          direction="column"
          alignItems="center"
          style={{ minHeight: "100vh", marginBottom: "50vh" }}
        >
          <DropSelect
            label={"Kernel"}
            textHelper={"Select kernel"}
            value={kernel}
            handleChange={handleKernel}
            selectOptions={kernels.map((kernel) =>
              toSelectOptionKernel(kernel)
            )}
          />

          <DropSelect
            label={"DataSet"}
            textHelper={"Select dataSet"}
            value={dataSet}
            handleChange={handleDataSet}
            selectOptions={dataSets.map((dataSet) =>
              toSelectOptionDataSet(dataSet)
            )}
          />

          <MultipleSelectChip
            label={"C"}
            textHelper={"Select C values"}
            options={cOptions.map((element) => element.value)}
            value={c}
            onChange={handleC}
          />

          <NumberField label={"CV"} value={cv} onChange={handleCv} />

          <NumberField
            label={"Experiments"}
            value={experiments}
            onChange={handleExperiments}
          />

          <MultipleSelectChip
            label={"Parameters"}
            textHelper={"Select parameters"}
            options={
              typeof kernelOptions === "undefined"
                ? []
                : (kernelOptions as string[])
            }
            value={parameters}
            onChange={handleParameters}
          />

          <Box sx={{ m: 1, minWidth: 400, padding: "10px" }}>
            <Grid container spacing={1}>
              <Grid item key={0}>
                <FormControlLabel
                  value="start"
                  control={<Checkbox checked={rbf} onChange={handleRbf} />}
                  label="Rbf"
                  labelPlacement="start"
                />
              </Grid>

              <Grid item key={1}>
                <FormControlLabel
                  value="start"
                  control={
                    <Checkbox checked={normalize} onChange={handleNormalize} />
                  }
                  label="Normalize"
                  labelPlacement="start"
                />
              </Grid>
              <Grid item key={2}>
                <FormControlLabel
                  value="start"
                  control={
                    <Checkbox
                      checked={withLabels}
                      onChange={handleWithLabels}
                    />
                  }
                  label="With labels"
                  labelPlacement="start"
                />
              </Grid>

              <Grid item key={3}>
                <FormControlLabel
                  value="start"
                  control={
                    <Checkbox
                      checked={withAttributes}
                      onChange={handleWithAttributes}
                    />
                  }
                  label="With attributes"
                  labelPlacement="start"
                />
              </Grid>
            </Grid>
          </Box>
          
          {rbf ? (
            <MultipleSelectChip
              label={"Sigma"}
              textHelper={"Select sigma values"}
              options={sigmaOptions.map((element) => element.label)}
              value={sigma}
              onChange={handleSigma}
            />
          ) : (
            <div />
          )}

          <Button
            variant="contained"
            sx={{ m: 1, minWidth: 400, padding: "10px", marginTop: "50px" }}
            onClick={handleRunClassification}
          >
            Run
          </Button>
        </Grid>
      )}
    </div>
  );
};

export default Classification;

package org.hsm.hmi;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;

import java.io.Serializable;
import java.util.List;

public class TextOutput implements Serializable {
    private List<ModuleStringModel> models;
    public TextOutput(List<ModuleStringModel> models) {
        this.models = models;
    }

    public List<ModuleStringModel> getModels() {
        return models;
    }

    public void setModels(List<ModuleStringModel> models) {
        this.models = models;
    }

    public String asJSON() throws JsonProcessingException {
        for (ModuleStringModel model: models) {
            model.prepareForOutput();
        }

        var mapper = new ObjectMapper().enable(SerializationFeature.INDENT_OUTPUT);
        return mapper.writeValueAsString(this);
    }
}
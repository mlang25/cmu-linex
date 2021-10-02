package com.sourcactus.cmulinex.ui.main

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.Transformations
import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import java.lang.Math.floor
import java.lang.Math.round

class ListingViewModel : ViewModel() {

    private val _index = MutableLiveData<Int>()
    private val _name = MutableLiveData<String>()
    private val _time = MutableLiveData<Double>()
    val text: LiveData<String> = Transformations.map(_index) {
        "Hello world from, section: $it"
    }

    val nameInfo: LiveData<String> = Transformations.map(_name) {
        "$it (${_index.value}): \n ${round(floor(_time.value!!))} minutes,  ${round(60 * (_time.value!! - floor(_time.value!!)))} seconds"
    }

    fun setIndex(index: Int) {
        _index.value = index
    }

    fun setName(name: String) {
        _name.value = name
    }

    fun setTime(time: Double) {
        _time.value = time
    }
}
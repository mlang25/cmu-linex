package com.sourcactus.cmulinex

import android.content.Context
import android.content.SharedPreferences
import android.os.Bundle
import com.google.android.material.floatingactionbutton.FloatingActionButton
import com.google.android.material.snackbar.Snackbar
import com.google.android.material.tabs.TabLayout
import androidx.viewpager.widget.ViewPager
import androidx.appcompat.app.AppCompatActivity
import android.view.Menu
import android.view.MenuItem
import android.view.View
import android.widget.CalendarView
import android.widget.EditText
import android.widget.Toast
import androidx.fragment.app.Fragment
import com.android.volley.AuthFailureError
import com.android.volley.Request
import com.android.volley.toolbox.JsonObjectRequest
import com.android.volley.toolbox.Volley
import com.sourcactus.cmulinex.ui.main.ListItemFragment
import com.sourcactus.cmulinex.ui.main.SectionsPagerAdapter
import org.json.JSONObject
import java.util.*

class MainActivity : AppCompatActivity() {
    final var RESTAURANT_NAME = "restaurant_name"
    final var START_TIME = "start_time"
    private lateinit var sharedPreferences: SharedPreferences
    private lateinit var editor: SharedPreferences.Editor

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        val sectionsPagerAdapter = SectionsPagerAdapter(this, supportFragmentManager)
        val viewPager: ViewPager = findViewById(R.id.view_pager)
        viewPager.adapter = sectionsPagerAdapter
        val tabs: TabLayout = findViewById(R.id.tabs)
        tabs.setupWithViewPager(viewPager)
        sharedPreferences = this.getPreferences(Context.MODE_PRIVATE)
        editor = sharedPreferences.edit()

    }

    fun startTiming(view: View) {
        val restaurantInput: EditText = this.findViewById(R.id.facility)
        val restaurantName = restaurantInput.text.toString()
        val calendar: Calendar = Calendar.getInstance()
        editor.putString(RESTAURANT_NAME, restaurantName)
        editor.putLong(START_TIME, calendar.timeInMillis)
        editor.apply()
        editor.commit()
        Toast.makeText(this, "Timing started!", 500).show()
    }

    fun endTiming(view: View) {
        val namesList: Array<String> = view.context.resources.getStringArray(R.array.restaurants_array)
        val calendar: Calendar = Calendar.getInstance()
        val startTime = sharedPreferences.getLong(START_TIME, -1)
        val badValue:Long = -1
        if(startTime == badValue) {
            return
        }
        val diningName = sharedPreferences.getString(RESTAURANT_NAME, "NONE") ?: "NONE"
        var diningId = diningName.toIntOrNull() ?: -1

        if(diningId == -1 || diningId >= namesList.size) {

            for(i in 0..namesList.size - 1) {
                if(namesList[i].contains(diningName, ignoreCase = true)) {
                    diningId = i
                    break
                }
            }

        }
        editor.putLong(START_TIME, -1)
        editor.apply()
        editor.commit()
        if(diningId == -1) {
            return
        }

        val timeDiff:Double = (calendar.timeInMillis - startTime) / 60000.0
        val reqQueue = Volley.newRequestQueue(this)
        val url = "http://67.207.94.22:5000/submit"
        val jsonParams = JSONObject()
        jsonParams.put("res_id", diningId)
        jsonParams.put("wait_time", timeDiff)
        System.out.println(jsonParams.toString())
        val jsonObjectRequest = JsonObjectRequest(
            Request.Method.POST, url, jsonParams,
            { response ->
                System.out.println("POSTED " + response.toString())
            },
            { error ->
                error.printStackTrace()
                // TODO: Handle error
            }
        )

        reqQueue.add(jsonObjectRequest)

    }
}
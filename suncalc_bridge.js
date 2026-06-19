#!/usr/bin/env node
/**
 * Node.js bridge for suncalc library
 * Takes JSON input via stdin and outputs JSON results
 */

import * as SunCalc from 'suncalc';

function processInput() {
    let input = '';
    
    process.stdin.on('data', chunk => {
        input += chunk;
    });
    
    process.stdin.on('end', () => {
        try {
            const params = JSON.parse(input);
            const date = params.date ? new Date(params.date) : new Date();
            const lat = parseFloat(params.lat);
            const lng = parseFloat(params.lng);
            
            if (isNaN(lat) || isNaN(lng)) {
                throw new Error('Invalid latitude or longitude');
            }
            
            // Get sun times
            const times = SunCalc.getTimes(date, lat, lng);
            
            // Get moon times
            const moonTimes = SunCalc.getMoonTimes(date, lat, lng);
            
            // Get moon illumination
            const moonIllumination = SunCalc.getMoonIllumination(date);
            
            // Get sun position at noon
            const sunPos = SunCalc.getPosition(date, lat, lng);
            
            // Get moon position
            const moonPos = SunCalc.getMoonPosition(date, lat, lng);
            
            // Format times to ISO strings (handle nulls)
            const formatTime = (time) => time ? time.toISOString() : null;
            
            const result = {
                date: date.toISOString(),
                location: { lat, lng },
                sun: {
                    times: {
                        nadir: formatTime(times.nadir),
                        nightEnd: formatTime(times.nightEnd),
                        nauticalDawn: formatTime(times.nauticalDawn),
                        dawn: formatTime(times.dawn),
                        sunrise: formatTime(times.sunrise),
                        sunriseEnd: formatTime(times.sunriseEnd),
                        goldenHourEnd: formatTime(times.goldenHourEnd),
                        solarNoon: formatTime(times.solarNoon),
                        goldenHour: formatTime(times.goldenHour),
                        sunsetStart: formatTime(times.sunsetStart),
                        sunset: formatTime(times.sunset),
                        dusk: formatTime(times.dusk),
                        nauticalDusk: formatTime(times.nauticalDusk),
                        night: formatTime(times.night)
                    },
                    position: {
                        altitude: sunPos.altitude,
                        azimuth: sunPos.azimuth
                    },
                    alwaysUp: times.alwaysUp || false,
                    alwaysDown: times.alwaysDown || false
                },
                moon: {
                    times: {
                        rise: formatTime(moonTimes.rise),
                        set: formatTime(moonTimes.set)
                    },
                    illumination: {
                        fraction: moonIllumination.fraction,
                        phase: moonIllumination.phase,
                        angle: moonIllumination.angle,
                        waxing: moonIllumination.waxing
                    },
                    position: {
                        altitude: moonPos.altitude,
                        azimuth: moonPos.azimuth,
                        distance: moonPos.distance,
                        parallacticAngle: moonPos.parallacticAngle
                    },
                    alwaysUp: moonTimes.alwaysUp || false,
                    alwaysDown: moonTimes.alwaysDown || false
                }
            };
            
            console.log(JSON.stringify(result, null, 2));
        } catch (error) {
            console.error(JSON.stringify({ error: error.message }));
            process.exit(1);
        }
    });
}

processInput();

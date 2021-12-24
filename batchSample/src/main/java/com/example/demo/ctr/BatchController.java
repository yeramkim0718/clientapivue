package com.example.demo.ctr;

import static org.quartz.JobBuilder.newJob;

import java.util.HashMap;
import java.util.Map;

import javax.annotation.PostConstruct;

import org.quartz.CronScheduleBuilder;
import org.quartz.JobDataMap;
import org.quartz.JobDetail;
import org.quartz.Scheduler;
import org.quartz.SchedulerException;
import org.quartz.Trigger;
import org.quartz.TriggerBuilder;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;

import com.example.demo.job.TrReReqJob;

import lombok.extern.slf4j.Slf4j;

@Slf4j
@Controller
public class BatchController {

    @Autowired
    private Scheduler scheduler;
    

    @PostConstruct
    public void start() {

        JobDetail aggreReqJobDetail = buildJobDetail(TrReReqJob.class, "testJob", "test", new HashMap());
        try {
			scheduler.scheduleJob(aggreReqJobDetail, buildJobTrigger("0 * * * * ?"));
		} catch (SchedulerException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
    }

    //String scheduleExp ="0 40 11 * * ?"; 초 분 시 일 월 ?
    public Trigger buildJobTrigger(String scheduleExp) {
        return TriggerBuilder.newTrigger()
                .withSchedule(CronScheduleBuilder.cronSchedule(scheduleExp)).build();
    }

    public JobDetail buildJobDetail(Class job, String name, String group, Map params) {
        JobDataMap jobDataMap = new JobDataMap();
        jobDataMap.putAll(params);

        return newJob(job).withIdentity(name, group)
                .usingJobData(jobDataMap)
                .build();
    }
}
